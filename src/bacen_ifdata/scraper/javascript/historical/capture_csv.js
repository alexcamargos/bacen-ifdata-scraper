function captureCsv(month, scope, report, done) {
    if (selDataBase?.dt !== month || selTipoInst?.id !== scope ||
        selRelatorio?.trel?.id !== report || jQuery.active > 0) {
        done(null);
        return;
    }
    let blobUrl;
    const capture = event => {
        if (event.target.download === 'dados.csv') {
            event.preventDefault();
            blobUrl = event.target.href;
        }
    };
    document.addEventListener('click', capture, true);
    try {
        downloadCsv();
    } finally {
        document.removeEventListener('click', capture, true);
    }
    if (!blobUrl?.startsWith('blob:')) {
        done(null);
        return;
    }
    fetch(blobUrl).then(response => response.blob()).then(blob => {
        const reader = new FileReader();
        reader.onload = () => done(reader.result.split(',')[1]);
        reader.onerror = () => done(null);
        reader.readAsDataURL(blob);
    }).catch(() => done(null)).finally(() => URL.revokeObjectURL(blobUrl));
}
