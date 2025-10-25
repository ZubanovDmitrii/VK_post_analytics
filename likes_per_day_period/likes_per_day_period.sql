SELECT
	CASE
		WHEN DATE_PART ('hour', date) >= 4 AND DATE_PART('hour', date) < 12 THEN 2
		WHEN DATE_PART ('hour', date) >= 12 AND DATE_PART('hour', date) < 17 THEN 3
		WHEN DATE_PART ('hour', date) >= 17 AND DATE_PART('hour', date) < 23 THEN 4
	ELSE 1
	END AS day_period_number,
--Задаем номер для каждого времени суток (это нужно только для сортировки таблицы от 0 до 24 часов)
	CASE
		WHEN DATE_PART ('hour', date) >= 4 AND DATE_PART('hour', date) < 12 THEN 'Morning (4-11)'
		WHEN DATE_PART ('hour', date) >= 12 AND DATE_PART('hour', date) < 17 THEN 'Afternoon (12-16)'
		WHEN DATE_PART ('hour', date) >= 17 AND DATE_PART('hour', date) < 23 THEN 'Evening (17-23)'
	ELSE 'Night (0-3)'
	END AS day_period,
--Делим часы дня на периоды: ночь, утро, день, вечер
	SUM(likes_count) AS likes_count,
--Считаем количество лайков для последующей группировки по периодам дня
	COUNT(id) AS posts_count,
--Считаем количество постов для последующей группировки по периодам дня
	ROUND(SUM(likes_count)::DECIMAL / COUNT(id), 2) AS likes_per_post
--Считаем количество лайков на пост для последующей группировки по периодам дня
FROM posts
GROUP BY day_period, day_period_number
ORDER BY day_period_number