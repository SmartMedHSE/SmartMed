'use strict';

export const API = 'http://127.0.0.1:15001/api';

export const fetchGet = (
    path = '/',
    api = API,
) => {
    if (path.includes('undefined')) {
        throw new Error('bad path');
    }
    return fetch(`${api}/${path}`, {
        method: 'GET',
        credentials: 'include',
    });
};

export const fetchPost = (
    path = '/',
    body = null,
    api = API,
) => {
    if (path.includes('undefined')) {
        throw new Error('bad path');
    }
    return fetch(`${api}/${path}`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
        },
        body: JSON.stringify(body)
    });
};
