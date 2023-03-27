import axios, { AxiosRequestConfig } from 'axios';

import storage from './storage';

export const isAxiosError = axios.isAxiosError;

const axiosConfig: AxiosRequestConfig = {
    baseURL: "http://localhost:8080/",
    headers: {
        'Accept': 'application/json',
        //'Content-Type': 'application/json',
    },
};

export const axiosInstance = axios.create(axiosConfig);

axiosInstance.interceptors.request.use((config) => {
    const token = storage.getToken();
    const role = storage.getRole();

    if (token && role && config.headers) {
        config.headers['Authorization'] = `Bearer ${token}`;
        config.headers['Role'] = `${role}`;
    }

    return config;
});