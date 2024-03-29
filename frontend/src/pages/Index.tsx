import React, { useState } from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { Link as RouterLink } from "react-router-dom";
import LoadingButton from "@mui/lab/LoadingButton";
import validator from "validator";
import axios from "axios";
import UserData from "../components/UserData";
import Alert from "@mui/material/Alert";
import { UserDataType } from "../Interfaces";

interface formStateObject {
  isUsernameValid: boolean;
  isPasswordValid: boolean;
}
const baseFormValidity: formStateObject = {
  isUsernameValid: true,
  isPasswordValid: true,
};

export default function LogIn() {
  const [formState, setFormState] = useState<formStateObject>(baseFormValidity);
  const [reqErr, setReqErr] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [userData, setUserData] = useState<UserDataType>();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const data = {
      username: formData.get("username") as string,
      password: formData.get("password"),
    } as const;
    const isUsernameValid = data.username.length > 3;
    const isPasswordValid = validator.isStrongPassword(
      data.password as string,
      {
        minLength: 8,
        minNumbers: 1,
        minSymbols: 0,
        minUppercase: 0,
      }
    );

    setFormState({
      isUsernameValid: isUsernameValid,
      isPasswordValid: isPasswordValid,
    });
    if (!isUsernameValid || !isPasswordValid) return;

    setReqErr("");
    setLoading(true);

    try {
      const answer = await axios.post("http://localhost:5000/login", data);
      console.log(answer.data);
      setUserData(answer.data);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setReqErr(err.response!.data.description);
        setFormState({
          isUsernameValid: false,
          isPasswordValid: false,
        });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {userData === undefined ? (
        <Container component="main" maxWidth="xs">
          <CssBaseline />
          <Box
            sx={{
              marginTop: 8,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5" sx={{ mb: 2 }}>
              Sign in
            </Typography>
            {loading && (
              <LoadingButton
                loading
                size="large"
                variant="outlined"
                sx={{ p: 2 }}
              />
            )}
            {reqErr && (
              <Alert variant="filled" severity="error" sx={{ mb: 2 }}>
                {reqErr}
              </Alert>
            )}
            <Box
              component="form"
              onSubmit={handleSubmit}
              noValidate
              sx={{ mt: 1 }}
            >
              <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="Username"
                name="username"
                autoComplete="username"
                autoFocus
                error={!formState.isUsernameValid}
                helperText={
                  !formState.isUsernameValid
                    ? "You need to have a valid username."
                    : ""
                }
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
                error={!formState.isPasswordValid}
                helperText={
                  !formState.isPasswordValid
                    ? "Your password must contain at least 8 characters and minimum 1 Number"
                    : ""
                }
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign In
              </Button>
              <Grid container justifyContent="center" alignItems="center">
                <Link component={RouterLink} to="/signup">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Box>
          </Box>
        </Container>
      ) : (
        <UserData {...userData} />
      )}
    </>
  );
}
