SELECT DATE_PART('isodow', date) AS day_of_week_number,
--Получаем номер дня недели (для последующей сортировки)
TO_CHAR(date, 'Day') AS day_of_week,
--Получаем названия дней недели
SUM(likes_count) AS likes_count,
--Считаем количество лайков для группировки по дням недели
COUNT(id) AS posts_count,
--Считаем количество постов для группировки по дням недели
ROUND(SUM(likes_count)::DECIMAL / COUNT(id), 2) AS likes_per_post
--Считаем колличество лайков на пост для группировки по дням недели
FROM posts
GROUP BY day_of_week_number, day_of_week
ORDER BY day_of_week_number 