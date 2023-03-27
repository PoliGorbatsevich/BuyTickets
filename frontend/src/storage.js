const storage = {
    getToken: () => {
        try {
            return JSON.parse(
                window.localStorage.getItem(`token`)
        )
        } catch {
            return null;
        }
    },
    getRole: () => {
        try {
            return JSON.parse(
                window.localStorage.getItem(`role`)
            )
        } catch {
            return null;
        }
    },
    setToken: (token) => {
        window.localStorage.setItem(`token`, JSON.stringify(token));
    },
    setRole: (role) => {
        window.localStorage.setItem(`role`, JSON.stringify(role));
    },

    clearToken: () => {
        window.localStorage.removeItem(`token`);
    },
    clearAll: () => {
        window.localStorage.removeItem(`token`);
        window.localStorage.removeItem(`role`);
    },
};

export default storage;