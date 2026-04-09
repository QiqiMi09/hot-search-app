document.addEventListener('DOMContentLoaded', () => {
    const hotSearchesList = document.getElementById('hot-searches-list');
    const aiGeneratedContent = document.getElementById('ai-generated-content');
    const aiText = document.getElementById('ai-text');
    const aiImage = document.getElementById('ai-image');

    // Function to fetch and display hot searches
    async function fetchHotSearches() {
        try {
            const response = await fetch('/hot_searches');
            const searches = await response.json();
            hotSearchesList.innerHTML = ''; // Clear existing list
            searches.forEach(search => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `<span class="rank">${search.rank}.</span> <span class="title">${search.title}</span>`;
                listItem.addEventListener('click', () => selectHotSearch(search.title));
                hotSearchesList.appendChild(listItem);
            });
        } catch (error) {
            console.error('Error fetching hot searches:', error);
            hotSearchesList.innerHTML = '<li>加载热搜失败，请稍后再试。</li>';
        }
    }

    // Function to handle hot search selection and AI content generation
    async function selectHotSearch(title) {
        aiText.textContent = 'AI正在努力生成内容...';
        aiGeneratedContent.style.display = 'block';
        aiImage.style.display = 'none'; // Ensure image is hidden

        try {
            const response = await fetch('/generate_content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: title }),
            });
            const content = await response.json();
            if (response.ok) {
                aiText.textContent = content.text;
            } else {
                const errorMessage = content.error || 'AI生成内容失败。';
                if (errorMessage.includes('API调用失败 (429)')) {
                    aiText.textContent = 'AI生成内容失败：请求过于频繁，请稍后重试或检查您的OpenAI账户额度。';
                } else {
                    aiText.textContent = errorMessage + ' 请稍后再试。 ';
                }
            }
        } catch (error) {
            console.error('Error generating AI content:', error);
            aiText.textContent = 'AI生成内容失败，请稍后再试。'
        }
    }

    // Initial fetch of hot searches when the page loads
    fetchHotSearches();
});
