import axios from "axios";

export const ApiClient = () => {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    axios.defaults.withCredentials = true;

    return axios.create({
        baseURL: "http://localhost:8000/api"
    });
}