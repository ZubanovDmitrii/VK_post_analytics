SELECT 
	days_between_posts, 
	SUM(likes_count) AS likes_count,
	COUNT(id) AS posts_count,
	ROUND(SUM(likes_count)::DECIMAL / COUNT(id), 2) AS likes_per_post
FROM
(SELECT 
	COALESCE(DATE_PART ('days', AGE (LAG(date) OVER(), date)), 0) AS days_between_posts,
	--Считаем количество дней между постами
	likes_count,
	id
FROM posts) AS days_interval
GROUP BY days_between_posts
ORDER BY days_between_posts