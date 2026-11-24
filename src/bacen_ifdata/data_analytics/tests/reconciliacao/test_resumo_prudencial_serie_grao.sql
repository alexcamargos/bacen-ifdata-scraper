select escopo, codigo, data_base
from {{ ref('view_resumo_prudencial_serie') }}
group by escopo, codigo, data_base
having count(*) <> 1
