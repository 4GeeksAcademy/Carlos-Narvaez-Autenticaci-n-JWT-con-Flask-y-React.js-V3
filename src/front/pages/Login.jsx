import React, {useState} from "react"
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { useNavigate } from "react-router-dom";

export const Login = () => {
const navigate = useNavigate()
const { store, dispatch } = useGlobalReducer()

const [email, setEmail]= useState("")
const [password, setPassword]= useState("")


const handleSubmit = async (e)=>{
  e.preventDefault()

  try{
    const backendUrl = import.meta.env.VITE_BACKEND_URL;
    const response = await fetch(`${backendUrl}/api/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json" 
      },
      body: JSON.stringify({email, password})
    } )


    if(!response.ok){
            alert ("login failed, try again" )
      return 
    }

    const data = await response.json() 

    localStorage.setItem("token", data.token)
    localStorage.setItem("user", JSON.stringify(data.user)) //si es necesario

    dispatch({
      type: "login",
      payload: {
        token:data.token,
        user:data.user
      }
    })

    navigate("/demo") //debe llevar a una ruta protegida
    alert ("login sucessfull")


  } catch (error) {
    console.log(error);
    alert("login failed")
    
  }



}

  
  return (
    <div className="container">
      <h1>Login</h1>


      <form onSubmit={handleSubmit}>
        <div className="row mb-3">
          <label htmlFor="inputEmail3" className="col-sm-2 col-form-label">Email</label>
          <div className="col-sm-10">
            <input type="email" className="form-control" id="inputEmail3" value={email} onChange={(e)=>setEmail(e.target.value)} />
          </div>
        </div>
        <div className="row mb-3">
          <label htmlFor="inputPassword3" className="col-sm-2 col-form-label">Password</label>
          <div className="col-sm-10">
            <input type="password" className="form-control" id="inputPassword3" value={password} onChange={(e)=>setPassword(e.target.value)} />
          </div>
        </div>
        

        <button type="submit" className="btn btn-primary">Login</button>
      </form>
    </div>
  );
};