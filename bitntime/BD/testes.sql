-- show databases;
-- use projeto_bitntime;
-- TABELAS BANCO projeto_bitntime
-- -- -- -- -- -- -- -- -- -- -- -- -- SPRINT 1 -- -- -- -- -- -- -- -- -- -- -- --
--  select * from projeto_bitntime.usuarios;
-- -- -- -- -- -- -- -- -- -- -- -- -- SPRINT 2 -- -- -- -- -- -- -- -- -- -- -- --
 -- select * from projeto_bitntime.config_alerta;
-- -- -- -- -- -- -- -- -- -- -- -- -- SPRINT 3 -- -- -- -- -- -- -- -- -- -- -- --
 -- select * from projeto_bitntime.historico_alertas; 
 
select 
	u.email, 
    ha.* 
from projeto_bitntime.historico_alertas as ha
left join projeto_bitntime.config_alerta ca 
	on ca.id = ha.config_alerta_id
left join projeto_bitntime.usuarios as u 
	on u.id = ca.usuario_id
order by 3, 2 desc;
 
 
 
-- -- -- -- -- -- -- -- -- -- -- -- -- SPRINT 4 -- -- -- -- -- -- -- -- -- -- -- --
-- select * from projeto_bitntime.preco_btc order by 1 desc;


