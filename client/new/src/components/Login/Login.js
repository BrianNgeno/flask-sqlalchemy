import React, { useState } from "react";

function Login({onLogin}) {
//   const [name, setName] = useState("");
  const [email, setEmail] =useState("")
  function handleSubmit(e) {
    e.preventDefault();
    fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email}),
    })
      .then((r) => r.json())
      .then((user) => onLogin(user));
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      {/* <input
        type="text"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      */}
      <button type="submit">Login</button>
    </form>
  );
}
export default Login;
