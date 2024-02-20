import React from "react";

interface IUserData {
  data: string[];
}

const UserData: React.FC<IUserData> = (data) => {
  return <div>{data.data}</div>;
};

export default UserData;
