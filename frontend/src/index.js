import React from "react";
import * as ReactDOMClient from "react-dom/client";
import App from "./App"
import { BrowserRouter } from 'react-router-dom';
import "./css/main.css"
import {Toaster} from "react-hot-toast";


const app = ReactDOMClient.createRoot(document.getElementById("app"))
app.render(<BrowserRouter><Toaster reverseOrder={true}/><App/></BrowserRouter>)
