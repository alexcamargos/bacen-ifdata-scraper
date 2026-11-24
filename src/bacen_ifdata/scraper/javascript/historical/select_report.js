function selectReport(month, scope, report, expectedFiles, reuse) {
    const dateIndex = listaRelatorios.findIndex(entry => entry.dt === month);
    if (dateIndex < 0) return 'month not found';
    if (selDataBase?.dt !== month) selectDataBase(dateIndex);
    const scopeIndex = listaTipoInst.findIndex(entry => entry.id === scope);
    if (scopeIndex < 0) return 'institution scope not found';
    if (selTipoInst?.id !== scope) selectTipoInst(scopeIndex);
    const reportIndex = selDataBase.files.findIndex(({trel}) =>
        trel?.id === report && trel.s.some(entry => entry.id === scope)
    );
    if (reportIndex < 0) return 'report not found';
    const actualFiles = selDataBase.files.filter(({f}) =>
        f.split('/').pop().startsWith('dados')
    ).map(({f}) => f);
    const sameFiles = JSON.stringify(actualFiles.sort()) ===
        JSON.stringify(expectedFiles.sort());
    if (!sameFiles) {
        return 'the report data files differ from the catalog';
    }
    if (reuse && selDadosDataBase === month && selCadastro && selInfos &&
        selFiltros && selDados.length === actualFiles.length) {
        window.selRelatorio = selDataBase.files[reportIndex];
        $('#btnRelatorio').text(window.selRelatorio.trel.n);
        updateIfCompleted();
    } else {
        // Do not accept a table built using the previous report's metadata.
        window.selInfos = window.selCadastro = window.selFiltros = null;
        selectRelatorio(reportIndex);
    }
    return null;
}
