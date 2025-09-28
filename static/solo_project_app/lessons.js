  const lessonInput = document.getElementById('lesson-search');
        const lessonResults = document.getElementById('search-results');
        const searchUrl = "{% url 'search_lessons' %}";  

        lessonInput.addEventListener('keyup', function () {
            const query = this.value.trim();
            if (!query) {
                lessonResults.innerHTML = "";  
                return;
            }

            fetch(`${searchUrl}?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => {
                    lessonResults.innerHTML = '';
                    if (!data.lessons.length) {
                        lessonResults.innerHTML = '<p>No lessons found.</p>';
                        return;
                    }
                    data.lessons.forEach(lesson => {
                        const div = document.createElement('div');
                        div.classList.add('lesson-card');
                        div.innerHTML = `
                    <h4>${lesson.title}</h4>
                    <p>${lesson.description || ''}</p>
                    <a href="/view_course/${lesson.course_id}/lesson/${lesson.id}/">View Lesson</a>

                `;
                        lessonResults.appendChild(div);
                    });
                })
                .catch(err => console.error('Error fetching lessons:', err));
        });