import React, { useState } from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import LoadingButton from "@mui/lab/LoadingButton";
import Alert from "@mui/material/Alert";
import validator from "validator";
import axios from "axios";

interface formStateObject {
  isSenderValid: boolean;
  isPasswordValid: boolean;
  isReceiverValid: boolean;
  isAmountValid: boolean;
}
const baseFormValidity: formStateObject = {
  isSenderValid: true,
  isPasswordValid: true,
  isReceiverValid: true,
  isAmountValid: true,
};

export default function Transactions() {
  const [formState, setFormState] = useState<formStateObject>(baseFormValidity);
  const [reqErr, setReqErr] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [reqSuccess, setReqSuccess] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const data = {
      username: formData.get("sender") as string,
      password: formData.get("sender_password"),
      receiver: formData.get("receiver") as string,
      amount: formData.get("amount") as string,
    } as const;
    const isSenderValid = data.username.length > 3;
    const isPasswordValid = validator.isStrongPassword(
      data.password as string,
      {
        minLength: 8,
        minNumbers: 1,
        minSymbols: 0,
        minUppercase: 0,
      }
    );
    const isReceiverValid = data.receiver.length > 3;
    const isAmountValid = Number(data.amount) > 0;

    setFormState({
      isSenderValid: isSenderValid,
      isPasswordValid: isPasswordValid,
      isReceiverValid: isReceiverValid,
      isAmountValid: isAmountValid,
    });
    setReqSuccess(false);
    if (
      !isSenderValid ||
      !isPasswordValid ||
      !isReceiverValid ||
      !isAmountValid
    )
      return;

    setReqErr(false);
    setLoading(true);

    try {
      const answer = await axios.post(
        "http://localhost:5000/transactions",
        data
      );
      setReqSuccess(true);
      console.log(answer.data);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setReqErr(true);
        setFormState({
          isSenderValid: false,
          isPasswordValid: false,
          isReceiverValid: false,
          isAmountValid: false,
        });
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
          Make a Transaction
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
            Transaction is successfull
          </Alert>
        )}
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="sender"
            label="sender"
            name="sender"
            autoComplete="sender"
            autoFocus
            error={!formState.isSenderValid}
            helperText={
              !formState.isSenderValid
                ? "You need to have a valid username."
                : ""
            }
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="sender_password"
            label="Password"
            type="password"
            id="sender_password"
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
            name="receiver"
            label="Receiver"
            id="receiver"
            autoComplete="current-email"
            error={!formState.isReceiverValid}
            helperText={
              !formState.isReceiverValid ? "Please type correct username" : ""
            }
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="amount"
            label="Amount $"
            type="amount"
            id="amount"
            error={!formState.isAmountValid}
            helperText={
              !formState.isAmountValid ? "Please type correct amount" : ""
            }
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Send Money
          </Button>
        </Box>
      </Box>
      <Typography>You can always send money to Me! nika</Typography>
    </Container>
  );
}
