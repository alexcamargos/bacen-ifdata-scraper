select
    id_instituicao,
    id_data,
    count(*) as registros
from {{ ref('fato_resumo_financeiro') }}
group by id_instituicao, id_data
having count(*) > 1
