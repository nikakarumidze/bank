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
import Alert from "@mui/material/Alert";
import validator from "validator";
import axios from "axios";

interface formStateObject {
  isUsernameValid: boolean;
  isPasswordValid: boolean;
  isEmailValid: boolean;
}
const baseFormValidity: formStateObject = {
  isUsernameValid: true,
  isPasswordValid: true,
  isEmailValid: true,
};

export default function SignUp() {
  const [formState, setFormState] = useState<formStateObject>(baseFormValidity);
  const [reqErr, setReqErr] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [reqSuccess, setReqSuccess] = useState<boolean>(false);
  console.log(reqErr);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const data = {
      username: formData.get("username") as string,
      password: formData.get("password"),
      email: formData.get("email"),
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
    const isEmailValid = validator.isEmail(data.email as string);

    setFormState({
      isUsernameValid: isUsernameValid,
      isPasswordValid: isPasswordValid,
      isEmailValid: isEmailValid,
    });
    setReqSuccess(false);
    if (!isUsernameValid || !isPasswordValid || !isEmailValid) return;

    setReqErr("");
    setLoading(true);

    try {
      const answer = await axios.post("http://localhost:5000/signup", data);
      setReqSuccess(true);
      console.log(answer.data);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setReqErr(err.response!.data.description!.error);
        setFormState({
          isUsernameValid: false,
          isPasswordValid: false,
          isEmailValid: false,
        });
        console.log(err.response!.data);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
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
          Sign Up
        </Typography>
        {loading && (
          <LoadingButton
            loading
            size="large"
            variant="outlined"
            sx={{ p: 2 }}
          />
        )}
        {Boolean(reqErr) && (
          <Alert variant="filled" severity="error" sx={{ mb: 2 }}>
            {reqErr}
          </Alert>
        )}
        {reqSuccess && (
          <Alert variant="filled" severity="success" sx={{ mb: 2 }}>
            User Registered successfully
          </Alert>
        )}
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
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
          <TextField
            margin="normal"
            required
            fullWidth
            name="email"
            label="Email"
            type="Email"
            id="email"
            autoComplete="current-email"
            error={!formState.isEmailValid}
            helperText={
              !formState.isEmailValid ? "Please type correct Email" : ""
            }
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Register
          </Button>
          <Grid container justifyContent="center" alignItems="center">
            <Link component={RouterLink} to="/">
              {"Already have an account? Log In"}
            </Link>
          </Grid>
        </Box>
      </Box>
      <Typography mt={2} align="center" variant="h4" color="red">
        Register and get 5000$
      </Typography>
    </Container>
  );
}
