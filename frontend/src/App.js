import React from "react";
import Performancepage from "./pages/Performancepage"
import UserProfilepage from "./pages/UserProfilepage"
import NotFoundpage from "./pages/NotFoundpage";
import Layout from "./components/Layout"
import Authpage from "./pages/Authpage"
import {
    Routes,
    Route,
} from 'react-router-dom';
import Transactionpage from "./pages/Transactionpage";

class App extends React.Component {

    render () {
        return (
            <div>
                <Routes>
                    <Route path='/' element={<Layout/>}>
                        <Route path='/' element = {<Performancepage/>}/>
                        <Route path='/performance' element = {<Performancepage/>}/>
                        <Route path='/user_profile' element = {<UserProfilepage/>}/>
                        <Route path='/transaction_history' element = {<Transactionpage/>}/>
                        <Route path='/auth' element = {<Authpage />}/>
                        <Route path='*' element = {<NotFoundpage/>} />
                    </Route>
                </Routes>
            </div>
        )
    }
}

export default App