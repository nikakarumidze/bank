import { AppBar, Container } from "@mui/material";
import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <AppBar position="static">
      <Container
        sx={{
          py: 2,
          color: "white",
          justifyContent: "space-between",
          display: "flex",
        }}
      >
        <Link to="/">Home Page</Link>
        <Link to="/transactions">Make a Transaction</Link>
      </Container>
    </AppBar>
  );
};

export default Header;
