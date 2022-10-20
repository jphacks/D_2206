import axios from "./axios";

const newsApi = {
  test: () => axios.get("/"),
  entryURL: (params) => axios.post("/entryURL", params),
};

export default newsApi;
