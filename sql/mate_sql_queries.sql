SELECT 
	DATE_TRUNC('week', leads.created_at) AS week, 
    courses.type, 
    COUNT(leads.id) AS lead_count
FROM leads
JOIN courses ON leads.course_id = courses.id
GROUP BY week, courses.type;


SELECT 
   	domains.country_name,
	COUNT(leads.id) AS won_flex_leads
FROM leads
JOIN courses 
ON leads.course_id = courses.id
JOIN users 
ON leads.user_id = users.id
JOIN domains 
ON users.domain_id = domains.id
WHERE leads.status = 'WON'
	AND courses.type = 'FLEX'
	AND leads.created_at >= TIMESTAMP '2024-01-01 00:00:00 UTC'
GROUP BY domains.country_name
ORDER BY won_flex_leads DESC;


SELECT
	users.email AS email,
	leads.id AS lead_id,
	leads.lost_reason AS lost_reason
FROM leads
JOIN users
ON leads.user_id = users.id
JOIN courses
ON leads.course_id = courses.id
WHERE leads.status = 'LOST'
	AND courses.type = 'FLEX'
	AND leads.updated_at >= TIMESTAMP '2024-01-07 00:00:00 UTC';