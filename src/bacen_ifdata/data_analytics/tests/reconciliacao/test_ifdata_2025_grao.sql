select escopo, relatorio, data_base, linha, ordem_coluna
from {{ ref('fato_ifdata_2025_campos') }}
group by escopo, relatorio, data_base, linha, ordem_coluna
having count(*) <> 1
    or data_base < date '2025-01-01'
