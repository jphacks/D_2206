import React, { useEffect, useState } from "react";
import { Box, Button, TextField } from "@mui/material";
import { Container } from "@mui/system";
import { LoadingButton } from "@mui/lab";
import newsApi from "../api/newsApi";

const Home = () => {
  const [results, setResults] = useState([]);
  const [test, setTest] = useState("何もないよ");
  const [url, setUrl] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("submit");

    const res = await newsApi.test();
    console.log(res);

    setResults([
      { methood: "success", hogehoeg: "hugahuga" },
      { methood: "dekita", "nya-": "wanwan" },
    ]);
  };

  return (
    <>
      <Container component="main" maxWidth="xs">
        <Box component="form" onSubmit={handleSubmit}>
          <TextField sx={{ mt: 7, width: 500 }} id="url" label="URL" name="url" value={url} onChange={(e) => setUrl(e.target.value)} required />
          <Box sx={{ display: "flex", justifyContent: "space-between" }}>
            <LoadingButton sx={{ mt: 7, width: 200 }} type="submit" variant="outlined">
              みる！！
            </LoadingButton>
            <LoadingButton sx={{ ml: 7, mt: 7, width: 200 }} onClick={() => setUrl("")} variant="outlined">
              clear
            </LoadingButton>
          </Box>
        </Box>

        {/*if(results.lenght !== 0)  {
        <Box >
        <TextField sx={{ mt: 7, width: 500 }} id="url" label="URL" name="url" required />
      </Box>
      }*/}
      </Container>
    </>
  );
};

export default Home;
