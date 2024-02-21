import {
  Container,
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import React from "react";
import { UserDataType } from "../Interfaces";

interface IUserData {
  data: UserDataType;
}

const UserData: React.FC<IUserData> = ({ data }) => {
  const transactions = data[1].map((item, i) => (
    <ListItem key={i}>
      <ListItemText>{item}</ListItemText>
      {/* <Typography>from {item}</Typography> */}
    </ListItem>
  ));
  return (
    <Container>
      <Box>
        <Typography>Balance - {data[0]} $</Typography>
      </Box>
      <Box>
        <Typography variant="h2">Transaction List</Typography>
        <List>{transactions}</List>
      </Box>
    </Container>
  );
};

export default UserData;
