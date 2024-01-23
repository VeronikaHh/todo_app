
function completeTask(taskId) {
    // Simulate clicking the corresponding badge link
    const badgeLink = document.getElementById(`completedBadge${taskId}`).querySelector('a');
    badgeLink.click();
}
