import { useState, useEffect } from 'react';

export function useQueryParams() {
    const [params, setParams] = useState({
        url: null, titulo: null, periodicode: null, fechaDesde: null, fechaHasta: null,
    });

    useEffect(() => {
        const sp = new URLSearchParams(window.location.search);
        setParams({
            url:         sp.get('url'),
            titulo:      sp.get('titulo'),
            periodicode: sp.get('periodicode'),
            fechaDesde:  sp.get('fechaDesde'),
            fechaHasta:  sp.get('fechaHasta'),
        });
    }, []);

    return params;
}
