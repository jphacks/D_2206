import React, { useEffect, useState } from "react";
import { Box, Button, TextField } from "@mui/material";
import { Container } from "@mui/system";
import { LoadingButton } from "@mui/lab";
import newsApi from "../api/newsApi";

const Home = () => {
  const [results, setResults] = useState([]);
  const [url, setUrl] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    const url = data.get("url");

    const res = await newsApi.test();
    const res_1 = await newsApi.entryURL({ url });
    console.log(res.results);
    console.log(res.results[0]);
    console.log(res.results[1]);

    setResults(res.results);
    console.log(results);
  };

  return (
    <>
      <Container component="main">
        <h1> 曖昧警察だ！！！！</h1>
        <Box component="form" onSubmit={handleSubmit} maxWidth="1000">
          <TextField sx={{ mt: 7, width: 1150 }} id="url" label="URL" name="url" value={url} onChange={(e) => setUrl(e.target.value)} required />
          <Box sx={{ mt: 3, display: "flex", justifyContent: "space-between" }}>
            <LoadingButton sx={{ width: 200 }} type="submit" variant="outlined">
              みる！！
            </LoadingButton>
            <LoadingButton sx={{ width: 200 }} onClick={() => setUrl("")} variant="outlined">
              clear
            </LoadingButton>
          </Box>
        </Box>

        <Box sx={{ mt: 3, ml: "50%" }}>結果</Box>

        {results.length === 0 ? (
          <div>0やで</div>
        ) : (
          <Box sx={{ mt: 5, border: 1 }}>
            <p>
              {results.map((item) => {
                return <span style={{ color: item.color }}>{item.text}</span>;
              })}
            </p>
          </Box>
        )}
      </Container>
    </>
  );
};

export default Home;
