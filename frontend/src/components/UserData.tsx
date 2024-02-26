import {
  Container,
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { UserDataType } from "../Interfaces";

const UserData: React.FC<UserDataType> = ({ balance, transactions }) => {
  const allTransactions = transactions.map((transaction, i) => (
    <TableRow
      key={i}
      sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
    >
      {transaction.map((attr, i) => (
        <TableCell align="right" key={String(attr) + String(i)}>
          {attr}
        </TableCell>
      ))}
    </TableRow>
  ));
  return (
    <Container>
      <Box>
        <Typography my={2}>Balance - {balance} $</Typography>
      </Box>
      <Box>
        <Typography variant="h2">Transaction List</Typography>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell align="right">Sender</TableCell>
                <TableCell align="right">Receiver&nbsp;</TableCell>
                <TableCell align="right">Amount&nbsp;</TableCell>
                <TableCell align="right">Date&nbsp;</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>{allTransactions}</TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Container>
  );
};

export default UserData;
