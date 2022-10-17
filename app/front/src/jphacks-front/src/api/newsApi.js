import axios from "./axios";

const newsApi = {
  test: () => axios.get("/"),
};

export default newsApi;
