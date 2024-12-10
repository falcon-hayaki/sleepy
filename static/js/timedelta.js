let totalSeconds = 0;

function updateTime() {
    if (totalSeconds < 0) document.getElementById('record_time').innerText = "已经过去了: 未知时间";

    let days = Math.floor(totalSeconds / (3600 * 24)); // 计算天数
    let hours = Math.floor((totalSeconds % (3600 * 24)) / 3600); // 计算小时数
    let minutes = Math.floor((totalSeconds % 3600) / 60); // 计算分钟数
    let seconds = totalSeconds % 60; // 计算秒数

    let timeParts = [];
    
    if (days > 0) timeParts.push(`${days}天`);
    if (hours > 0 || days > 0) timeParts.push(`${hours}小时`);
    if (minutes > 0 || hours > 0 || days > 0) timeParts.push(`${minutes}分钟`);
    if (seconds > 0 || minutes > 0 || hours > 0 || days > 0) timeParts.push(`${seconds}秒`);
    
    document.getElementById('record_time').innerText = "已经过去了： " + timeParts.join(" ");
    
    totalSeconds++;
}

function startTimer(seconds) {
    totalSeconds = seconds;
    setInterval(updateTime, 1000);
}
