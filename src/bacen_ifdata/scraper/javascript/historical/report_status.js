function reportStatus(month, scope, report, requiredFiles) {
    if (jQuery.active > 0) return null;
    if (selDataBase?.dt !== month || selTipoInst?.id !== scope ||
        selRelatorio?.trel?.id !== report) {
        return `selection changed to ${selDataBase?.dt}/${selTipoInst?.id}/` +
            `${selRelatorio?.trel?.id}`;
    }
    if (selDadosDataBase !== month || selDados.length !== requiredFiles ||
        !selCadastro || !selInfos || !selFiltros) return 'source data incomplete';
    if (!table?.rows?.length || !csvHeaderLines.length ||
        document.getElementById('divExport').style.display === 'none') {
        return 'report table is empty';
    }
    return 'ready';
}
