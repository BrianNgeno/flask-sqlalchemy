import "./App.css";
import React, { useEffect, useState } from "react";
import { useFormik } from "formik";
import * as yup from "yup";
import Login from "./components/Login/Login";

function App() {
  const [users, setUsers] = useState([{}]);
  const [refreshPage, setRefreshPage] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/checksession").then((r) => {
      if (r.ok) {
        r.json().then((users) => setUsers(users));
      }
    });
  }, []);

  useEffect(() => {
    //fetch
    fetch("http://127.0.0.1:5000/users")
      .then((response) => response.json())
      .then((users) => setUsers(users));
  }, [refreshPage]);

  function handleLogin(users) {
    setUsers(users);
  }

  const formSchema = yup.object().shape({
    name: yup.string().required("Name input is required").max(20),
    email: yup.string().email("Invalid email").required("Email is required"),
  });

  const formik = useFormik({
    initialValues: {
      name: "",
      email: "",
    },
    validationSchema: formSchema,
    onSubmit: (values) => {
      console.log(values);
      fetch("http://127.0.0.1:5000/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values, null, 2),
      }).then((res) => {
        if (res.status === 201) {
          setRefreshPage(!refreshPage);
        } else {
          console.log("error");
        }
      });
    },
  });

  if (users) {
    return <h2>{users.email}</h2>;
  } else {
    return (
      <div className="App">
        <Login onLogin={handleLogin} />
        <h1>Signup Form</h1>
        <form onSubmit={formik.handleSubmit}>
          <label htmlFor="email">Email</label>
          <br />
          <input
            id="email"
            name="email"
            onChange={formik.handleChange}
            value={formik.values.email}
          />
          <p style={{ color: "red", fontSize: "10px" }}>
            {formik.errors.email}
          </p>
          <label htmlFor="name">Name</label>
          <br />
          <input
            id="name"
            name="name"
            onChange={formik.handleChange}
            value={formik.values.name}
          />
          <p style={{ color: "red", fontSize: "10px" }}>{formik.errors.name}</p>
          <button type="submit">submit</button>
        </form>

        {/* <table>
        <tbody style={{padding:'15px', color:"blue"}}>
          <tr>
            <th>Name</th>
            <th>Email</th>
          </tr>
          {users === "undefined" ? (
             <p>Loading</p>
          ) : (
            users.map((user,i)=>(
              <>
              <tr key={i}>
    
                <td>{user.name}</td>
                <td>{user.email}</td>
              </tr>
              </>
            ))
          )}
        </tbody>
      </table> */}
      </div>
    );
  }
}
export default App;
