let currentSource = "all";
let autoRefresh = true;
let refreshTimer = null;
let allData = {};
let expandedItems = new Set();
let currentTimePeriod = "all";
let searchQuery = "";
let previousAiCount = 0; // 用于检测新AI内容
const REFRESH_INTERVAL = 60 * 1000;

const content = document.getElementById("content");
const autoRefreshToggle = document.getElementById("autoRefresh");
const refreshBtn = document.getElementById("refreshBtn");
const statusText = document.getElementById("statusText");
const pageTitle = document.getElementById("pageTitle");
const totalCount = document.getElementById("totalCount");
const aiCount = document.getElementById("aiCount");
const timeFilter = document.getElementById("timeFilter");
const toastEl = document.getElementById("toast");
const toastMsg = document.getElementById("toastMsg");
const searchInput = document.getElementById("searchInput");
const hamburger = document.getElementById("hamburger");
const sidebar = document.getElementById("sidebar");
const sidebarOverlay = document.getElementById("sidebarOverlay");
const mobileNav = document.getElementById("mobileNav");

// ===== 推送通知系统 =====
let notificationPermission = false;
let knownAiTitles = new Set(); // 已知的AI内容标题
let isFirstLoad = true;

// 请求通知权限
async function requestNotificationPermission() {
    if (!("Notification" in window)) return false;
    if (Notification.permission === "granted") {
        notificationPermission = true;
        return true;
    }
    if (Notification.permission !== "denied") {
        const permission = await Notification.requestPermission();
        notificationPermission = permission === "granted";
        if (notificationPermission) showToast("通知已开启", "success");
        return notificationPermission;
    }
    return false;
}

// 发送桌面通知
function sendNotification(title, body, url) {
    if (!notificationPermission || Notification.permission !== "granted") return;
    const notification = new Notification(title, {
        body: body,
        icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%230a0b0f'/><text x='50' y='65' font-size='50' text-anchor='middle' fill='%2300f0ff'>⚡</text></svg>",
        tag: "ai-radar-" + Date.now(),
        requireInteraction: true,
    });
    notification.onclick = () => {
        window.focus();
        if (url) window.open(url, "_blank");
        notification.close();
    };
}

// 检测新AI内容并推送
function checkAndNotifyNewAI(newAiCount, newItems) {
    if (isFirstLoad) {
        // 首次加载，记录所有已知标题
        if (newItems) {
            newItems.forEach(item => knownAiTitles.add(item.title));
        }
        previousAiCount = newAiCount;
        isFirstLoad = false;
        return;
    }

    // 找出新增的AI内容
    const newAiItems = [];
    if (newItems) {
        newItems.forEach(item => {
            if (!knownAiTitles.has(item.title)) {
                newAiItems.push(item);
                knownAiTitles.add(item.title);
            }
        });
    }

    if (newAiItems.length > 0) {
        // 逐条推送新内容
        newAiItems.slice(0, 3).forEach((item, idx) => {
            setTimeout(() => {
                sendNotification(
                    `🔥 AI热点 #${idx + 1}`,
                    item.title,
                    item.url
                );
            }, idx * 1000);
        });
        // 如果超过3条，显示汇总
        if (newAiItems.length > 3) {
            setTimeout(() => {
                sendNotification(
                    "📊 更多AI热点",
                    `还有 ${newAiItems.length - 3} 条新内容`,
                    ""
                );
            }, 3000);
        }
    }

    previousAiCount = newAiCount;
}

// 页面加载时请求通知权限
document.addEventListener("DOMContentLoaded", () => {
    // 延迟请求，避免干扰用户体验
    setTimeout(() => {
        requestNotificationPermission();
    }, 3000);
});

// Mobile hamburger menu
function toggleSidebar() {
    sidebar.classList.toggle("open");
}

hamburger.addEventListener("click", toggleSidebar);
sidebarOverlay.addEventListener("click", () => sidebar.classList.remove("open"));

// Mobile quick nav
document.querySelectorAll(".mobile-nav-item").forEach((btn) => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".mobile-nav-item").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        // Also sync sidebar nav
        document.querySelectorAll(".nav-item").forEach((b) => b.classList.remove("active"));
        const source = btn.dataset.source;
        document.querySelector(`.nav-item[data-source="${source}"]`)?.classList.add("active");
        currentSource = source;
        pageTitle.textContent = titleMap[currentSource] || "RADAR";
        expandedItems.clear();
        timeFilter.style.display = currentSource === "ai" ? "flex" : "none";
        renderContent();
        sidebar.classList.remove("open");
    });
});

// 搜索过滤
searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    renderContent();
});

// 按Escape清空搜索
searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        searchInput.value = "";
        searchQuery = "";
        renderContent();
    }
});

// Toast通知
let toastTimer;
function showToast(msg, type = "info") {
    clearTimeout(toastTimer);
    toastEl.className = `toast ${type}`;
    toastMsg.textContent = msg;
    toastEl.classList.add("show");
    toastTimer = setTimeout(() => toastEl.classList.remove("show"), 3000);
}

// 骨架屏
function showSkeletons() {
    let html = '<div class="source-section"><div class="section-title">LOADING...</div><div class="source-grid">';
    for (let i = 0; i < 4; i++) {
        html += `<div class="skeleton-card">
            <div class="skeleton-header"><div class="skeleton-bar title"></div><div class="skeleton-bar time"></div></div>
            <div class="skeleton-bar line"></div><div class="skeleton-bar line short"></div>
            <div class="skeleton-bar line"></div><div class="skeleton-bar line short"></div>
            <div class="skeleton-bar line"></div><div class="skeleton-bar line short"></div>
        </div>`;
    }
    html += '</div></div>';
    content.innerHTML = html;
}

const titleMap = {
    all: "全部监控",
    ai: "AI 专题",
    weibo: "微博热搜",
    bilibili: "B站热搜",
    douyin: "抖音热搜",
    tiktok: "TikTok",
    github: "GitHub AI",
    hackernews: "HackerNews",
    qbitai: "量子位",
    arxiv: "ArXiv Papers",
    "36kr": "36Kr",
    history: "24H AI历史",
};

const HOT_SOURCES = ["weibo", "bilibili", "douyin", "tiktok", "36kr"];
const AI_SOURCES = ["github", "hackernews", "qbitai", "arxiv"];

// Nav buttons (sidebar)
document.querySelectorAll(".nav-item").forEach((btn) => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".nav-item").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        currentSource = btn.dataset.source;
        pageTitle.textContent = titleMap[currentSource] || "RADAR";
        expandedItems.clear();
        timeFilter.style.display = currentSource === "ai" ? "flex" : "none";
        // Sync mobile nav
        document.querySelectorAll(".mobile-nav-item").forEach((b) => b.classList.remove("active"));
        const mobileBtn = document.querySelector(`.mobile-nav-item[data-source="${currentSource}"]`);
        if (mobileBtn) mobileBtn.classList.add("active");
        renderContent();
        sidebar.classList.remove("open");
    });
});

// Time filter buttons
document.querySelectorAll(".time-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".time-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        currentTimePeriod = btn.dataset.period;
        renderAiView();
    });
});

autoRefreshToggle.addEventListener("change", (e) => {
    autoRefresh = e.target.checked;
    if (autoRefresh) {
        startAutoRefresh();
        statusText.textContent = "SYSTEM ONLINE";
    } else {
        stopAutoRefresh();
        statusText.textContent = "PAUSED";
    }
});

refreshBtn.addEventListener("click", () => loadData(true));

// 导出按钮
const exportBtn = document.getElementById("exportBtn");
exportBtn.addEventListener("click", () => {
    window.open("/api/export/csv?ai_only=true", "_blank");
    showToast("正在导出CSV...", "info");
});

function startAutoRefresh() {
    stopAutoRefresh();
    refreshTimer = setInterval(() => loadData(false), REFRESH_INTERVAL);
}

function stopAutoRefresh() {
    if (refreshTimer) { clearInterval(refreshTimer); refreshTimer = null; }
}

async function loadData(showSpinner = false) {
    if (showSpinner) {
        refreshBtn.classList.add("spinning");
        showToast("刷新中...");
    }
    try {
        const resp = await fetch("/api/hot/all");
        const json = await resp.json();
        if (json.code === 0) {
            allData = json.data;
            updateStats();
            renderContent();
            if (showSpinner) showToast("数据已更新", "success");
        }
    } catch (err) {
        showToast("网络错误", "error");
        content.innerHTML = `<div class="loading-state"><div class="terminal-loader"><span class="terminal-cursor"></span><span class="terminal-text">CONNECTION LOST</span></div></div>`;
    } finally {
        refreshBtn.classList.remove("spinning");
    }
}

function updateStats() {
    let total = 0, ai = 0;
    let allAiItems = [];
    for (const [source, info] of Object.entries(allData)) {
        if (source !== "ai") total += info.items.length;
        if (source === "ai" || AI_SOURCES.includes(source)) {
            ai += info.items.length;
            allAiItems = allAiItems.concat(info.items);
        }
    }
    totalCount.textContent = total;
    aiCount.textContent = ai;

    // 检测新AI内容并推送通知
    checkAndNotifyNewAI(ai, allAiItems);
}

function renderContent() {
    if (currentSource === "ai") { renderAiView(); return; }
    if (currentSource === "history") { renderHistoryView(); return; }

    if (currentSource !== "all") {
        const info = allData[currentSource];
        if (info) content.innerHTML = `<div class="source-grid">${renderCard(currentSource, titleMap[currentSource], info)}</div>`;
        return;
    }

    let html = '<div class="source-section"><div class="section-title">HOT SEARCH</div><div class="source-grid">';
    for (const s of HOT_SOURCES) { const info = allData[s]; if (info) html += renderCard(s, titleMap[s], info); }
    html += '</div></div>';

    html += '<div class="source-section"><div class="section-title">AI SOURCES</div><div class="source-grid">';
    for (const s of AI_SOURCES) { const info = allData[s]; if (info) html += renderCard(s, titleMap[s], info); }
    html += '</div></div>';

    content.innerHTML = html;
}

function filterByTime(items, period) {
    if (period === "all") return items;
    return items.filter((item) => !item.publish_time || isRecentEnough(item.publish_time, period));
}

function isRecentEnough(timeStr, period) {
    if (!timeStr) return true;
    if (timeStr.includes("分钟") || timeStr.includes("刚刚")) return true;
    if (timeStr.includes("小时")) return period !== "day" || (parseInt(timeStr) || 0) < 24;
    if (timeStr === "昨天") return true;
    if (timeStr.includes("天前")) { const d = parseInt(timeStr) || 0; return period === "day" ? false : period === "week" ? d <= 7 : true; }
    if (timeStr.includes("周前")) { return period === "month"; }
    if (timeStr.includes("个月前")) return (parseInt(timeStr) || 0) <= 1;
    return true;
}

function renderAiView() {
    const aiData = allData["ai"];
    if (!aiData) { content.innerHTML = `<div class="loading-state"><div class="terminal-loader"><span class="terminal-cursor"></span><span class="terminal-text">LOADING AI DATA...</span></div></div>`; return; }

    let items = filterByTime(aiData.items || [], currentTimePeriod);
    const labels = { all: "ALL", day: "24H", week: "7D", month: "30D" };

    let html = `<div class="ai-view"><div class="ai-header"><h2>⚡ AI TRENDING</h2><p>AGGREGATED · ${labels[currentTimePeriod]} · ${items.length} ITEMS</p></div>`;

    if (aiData.error) html += `<div class="source-error">FETCH FAILED</div>`;
    else if (items.length === 0) html += `<div class="source-error">NO AI ITEMS IN THIS PERIOD</div>`;
    else {
        html += `<div class="ai-list">`;
        items.forEach((item, idx) => { html += renderAiItem(item, idx + 1); });
        html += `</div>`;
    }
    html += `</div>`;
    content.innerHTML = html;
}

function renderAiItem(item, rank) {
    const rc = rank <= 3 ? ` top${rank}` : "";
    let meta = [];
    if (item.publish_time) meta.push(item.publish_time);
    if (item.author) meta.push(`@${item.author}`);
    if (item.views > 0) meta.push(`👁${formatNumber(item.views)}`);
    if (item.likes > 0) meta.push(`♥${formatNumber(item.likes)}`);
    if (item.comments > 0) meta.push(`💬${item.comments}`);
    const metaStr = meta.length ? meta.join(" · ") : item.extra;

    return `<a href="${item.url}" target="_blank" rel="noopener" class="ai-item"><span class="hot-rank${rc}">${rank}</span><div class="ai-info"><div class="ai-title">${esc(item.title)}</div><div class="ai-extra">${esc(metaStr)}</div></div>${item.hot_value > 0 ? `<span class="hot-value">${formatNumber(item.hot_value)}</span>` : ""}</a>`;
}

function renderCard(source, name, info) {
    let items = info.items;

    // 搜索过滤
    if (searchQuery) {
        items = items.filter(item =>
            item.title.toLowerCase().includes(searchQuery) ||
            (item.author && item.author.toLowerCase().includes(searchQuery)) ||
            (item.extra && item.extra.toLowerCase().includes(searchQuery))
        );
    }

    let h = `<div class="source-card"><div class="source-header"><span class="source-name ${source}">${name}</span><span class="source-time">${items.length}条</span></div>`;
    if (info.error) h += `<div class="source-error">FETCH FAILED</div>`;
    else if (!items.length) h += `<div class="source-error">${searchQuery ? "NO MATCH" : "NO DATA"}</div>`;
    else {
        h += `<ul class="hot-list">`;
        items.slice(0, 30).forEach((item, idx) => { h += renderItem(item, idx + 1, source); });
        h += `</ul>`;
    }
    return h + `</div>`;
}

function renderItem(item, displayRank, source) {
    const rc = displayRank === 1 ? " top1" : displayRank === 2 ? " top2" : displayRank === 3 ? " top3" : "";
    const isExpandable = source === "bilibili";
    const isExpanded = expandedItems.has(`${source}-${item.rank}`);
    const expandIcon = isExpandable ? `<span class="expand-icon${isExpanded ? " expanded" : ""}">▶</span>` : "";

    let label = "";
    // 热搜平台标签
    if (item.label && ["热", "新", "沸"].includes(item.label)) {
        const lc = item.label === "热" ? "hot" : item.label === "新" ? "new" : "boil";
        label = `<span class="item-label ${lc}">${item.label}</span>`;
    }
    // GitHub语言标签
    if (source === "github" && item.label) {
        label = `<span class="item-label lang">${item.label}</span>`;
    }
    // AI专源标签
    if (AI_SOURCES.includes(source) && item.is_ai_related) {
        label += `<span class="item-label ai">AI</span>`;
    }

    let meta = [];
    if (item.publish_time) meta.push(item.publish_time);
    if (item.author) meta.push(`@${item.author}`);
    if (item.views > 0) meta.push(`⭐${formatNumber(item.views)}`);
    if (item.likes > 0) meta.push(`🍴${formatNumber(item.likes)}`);
    if (item.comments > 0) meta.push(`💬${item.comments}`);
    const metaStr = meta.length ? meta.join(" · ") : item.extra;

    // 24小时历史视图
    function renderHistoryView() {
        let html = `<div class="ai-view"><div class="ai-header"><h2>⏱ 24H AI HISTORY</h2><p>PAST 24 HOURS · AI TOPICS FROM HOT SEARCH PLATFORMS</p></div>`;

        const platforms = ["bilibili", "weibo", "douyin"];
        const names = { bilibili: "B站", weibo: "微博", douyin: "抖音" };

        html += `<div class="source-grid">`;
        for (const plat of platforms) {
            const history = allData[plat]?.items?.filter(i => i.is_ai_related) || [];
            if (history.length > 0) {
                html += `<div class="source-card"><div class="source-header"><span class="source-name ${plat}">${names[plat]} AI历史</span><span class="source-time">${history.length}条</span></div>`;
                html += `<ul class="hot-list">`;
                history.slice(0, 20).forEach((item, idx) => {
                    html += `<a href="${item.url}" target="_blank" rel="noopener" class="hot-item clickable"><span class="hot-rank">${idx + 1}</span><div class="hot-info"><div class="hot-title">${esc(item.title)}</div><div class="hot-extra">${esc(item.extra)}</div></div></a>`;
                });
                html += `</ul></div>`;
            }
        }
        html += `</div></div>`;
        content.innerHTML = html;
    }

    const isClickable = ["36kr", "github", "hackernews", "qbitai"].includes(source) && item.url;
    if (isClickable) {
        return `<div class="hot-item-wrapper"><a href="${item.url}" target="_blank" rel="noopener" class="hot-item clickable"><span class="hot-rank${rc}">${displayRank}</span><div class="hot-info"><div class="hot-title">${esc(item.title)}${label}</div>${metaStr ? `<div class="hot-extra">${esc(metaStr)}</div>` : ""}</div></a></div>`;
    }

    return `<div class="hot-item-wrapper"><div class="hot-item${isExpandable ? " expandable" : ""}" data-source="${source}" data-rank="${item.rank}" data-title="${esc(item.title)}"><span class="hot-rank${rc}">${displayRank}</span><div class="hot-info"><div class="hot-title">${esc(item.title)}${label}</div>${metaStr ? `<div class="hot-extra">${esc(metaStr)}</div>` : ""}</div>${expandIcon}</div><div class="creators-panel" id="creators-${source}-${item.rank}"></div></div>`;
}

async function toggleCreators(source, rank, title) {
    const key = `${source}-${rank}`;
    const panel = document.getElementById(`creators-${key}`);
    const wrapper = panel?.closest(".hot-item-wrapper");
    const icon = wrapper?.querySelector(".expand-icon");

    if (expandedItems.has(key)) {
        expandedItems.delete(key);
        panel.innerHTML = "";
        panel.classList.remove("open");
        if (icon) icon.classList.remove("expanded");
        return;
    }

    expandedItems.add(key);
    if (icon) icon.classList.add("expanded");
    panel.innerHTML = `<div class="creators-loading">LOADING...</div>`;
    panel.classList.add("open");

    try {
        const resp = await fetch(`/api/bilibili/creators?keyword=${encodeURIComponent(title)}&limit=10`);
        const json = await resp.json();
        if (json.code === 0 && json.data.length > 0) {
            let h = `<div class="creators-header">CREATORS TOP ${json.data.length}</div><div class="creators-list">`;
            json.data.forEach((c, idx) => {
                h += `<a href="${c.video_url}" target="_blank" rel="noopener" class="creator-item"><span class="creator-rank">${idx + 1}</span><img class="creator-avatar" src="${c.avatar}" alt="${c.name}" onerror="this.style.display='none'"><div class="creator-info"><div class="creator-name">${esc(c.name)}</div><div class="creator-video">${esc(c.video_title)}</div></div><span class="creator-views">${formatNumber(c.view_count)}</span></a>`;
            });
            panel.innerHTML = h + `</div>`;
        } else {
            panel.innerHTML = `<div class="creators-empty">NO DATA</div>`;
        }
    } catch (err) {
        panel.innerHTML = `<div class="creators-empty">FAILED</div>`;
    }
}

document.addEventListener("click", (e) => {
    const item = e.target.closest(".hot-item.expandable");
    if (item) toggleCreators(item.dataset.source, parseInt(item.dataset.rank), item.dataset.title);
});

function fmtTime(iso) {
    if (!iso) return "";
    const d = new Date(iso);
    return `${d.getHours().toString().padStart(2, "0")}:${d.getMinutes().toString().padStart(2, "0")}:${d.getSeconds().toString().padStart(2, "0")}`;
}

function formatNumber(n) {
    if (n >= 1e8) return (n / 1e8).toFixed(1) + "亿";
    if (n >= 1e4) return (n / 1e4).toFixed(1) + "万";
    return n.toLocaleString();
}

function esc(s) { const d = document.createElement("div"); d.textContent = s || ""; return d.innerHTML; }

// ===== 移动端手势支持 =====
let touchStartX = 0;
let touchStartY = 0;

// 下拉刷新
let pullStartY = 0;
let isPulling = false;

document.addEventListener("touchstart", (e) => {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;

    // 下拉刷新检测
    if (window.scrollY === 0) {
        pullStartY = e.touches[0].clientY;
        isPulling = true;
    }
});

document.addEventListener("touchmove", (e) => {
    if (!isPulling) return;

    const pullDistance = e.touches[0].clientY - pullStartY;
    if (pullDistance > 60 && window.scrollY === 0) {
        // 显示下拉刷新提示
        if (!document.querySelector(".pull-refresh")) {
            const pullEl = document.createElement("div");
            pullEl.className = "pull-refresh";
            pullEl.textContent = "释放刷新";
            pullEl.style.cssText = "position:fixed;top:60px;left:50%;transform:translateX(-50%);background:var(--cyan);color:var(--bg-void);padding:8px 16px;border-radius:20px;font-size:12px;z-index:1000;";
            document.body.appendChild(pullEl);
        }
    }
});

document.addEventListener("touchend", (e) => {
    isPulling = false;
    const pullEl = document.querySelector(".pull-refresh");
    if (pullEl) {
        pullEl.remove();
        loadData(true);
        showToast("刷新中...");
    }

    // 左右滑动切换平台
    const touchEndX = e.changedTouches[0].clientX;
    const diffX = touchEndX - touchStartX;

    if (Math.abs(diffX) > 100 && Math.abs(diffX) > Math.abs(e.changedTouches[0].clientY - touchStartY)) {
        const sources = ["all", "ai", "weibo", "bilibili", "douyin", "github", "arxiv"];
        const currentIdx = sources.indexOf(currentSource);

        if (diffX < 0 && currentIdx < sources.length - 1) {
            // 左滑 - 下一个
            const nextSource = sources[currentIdx + 1];
            switchSource(nextSource);
        } else if (diffX > 0 && currentIdx > 0) {
            // 右滑 - 上一个
            const prevSource = sources[currentIdx - 1];
            switchSource(prevSource);
        }
    }
});

function switchSource(source) {
    currentSource = source;
    pageTitle.textContent = titleMap[source] || "RADAR";
    expandedItems.clear();
    timeFilter.style.display = source === "ai" ? "flex" : "none";

    // 同步导航状态
    document.querySelectorAll(".nav-item").forEach((b) => b.classList.remove("active"));
    document.querySelector(`.nav-item[data-source="${source}"]`)?.classList.add("active");
    document.querySelectorAll(".mobile-nav-item").forEach((b) => b.classList.remove("active"));
    document.querySelector(`.mobile-nav-item[data-source="${source}"]`)?.classList.add("active");

    renderContent();
}

// 检测移动端
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
if (isMobile) {
    document.body.classList.add("mobile");
}

showSkeletons();
loadData(true);
startAutoRefresh();
