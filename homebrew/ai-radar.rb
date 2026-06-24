class AiRadar < Formula
  desc "FastAPI Web Dashboard for AI Social Trends Radar"
  homepage "https://github.com/14sword/ai-radar"
  url "https://github.com/14sword/ai-radar/archive/refs/heads/main.tar.gz"
  version "1.0.0"

  depends_on "python"

  def install
    # Copy project files to libexec
    libexec.install Dir["*"]
    
    # Create virtualenv and install dependencies
    system "python3", "-m", "venv", libexec/"venv"
    system libexec/"venv/bin/pip", "install", "--upgrade", "pip"
    system libexec/"venv/bin/pip", "install", "-r", libexec/"requirements.txt"
    
    # Create bin runner script
    (bin/"ai-radar").write <<~EOS
      #!/bin/bash
      exec "#{libexec}/homebrew/ai-radar-launcher.sh" "$@"
    EOS
    chmod 0755, bin/"ai-radar"
  end

  service do
    run [opt_libexec/"venv/bin/python3", opt_libexec/"run.py"]
    keep_alive true
    working_dir opt_libexec
    log_path var/"log/ai-radar.log"
    error_log_path var/"log/ai-radar-err.log"
  end

  test do
    assert_match "AI Radar", shell_output("#{bin}/ai-radar --help", 1)
  end
end
