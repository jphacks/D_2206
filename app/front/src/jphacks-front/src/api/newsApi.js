import axios from "./axios";

const newsApi = {
  test: () => axios.get("/"),
  test_2: (params) => axios.post("/test", params),
};

export default newsApi;
