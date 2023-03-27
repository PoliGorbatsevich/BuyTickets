import {NavLink, Outlet} from 'react-router-dom';
import React from "react";
import DropdownMenu from './DropdownMenu';

class Layout extends React.Component{
    render(){
        return(
            <div>
                <header className="header">
                    <NavLink to="/performance" className="link">BuyTickets</NavLink>
                    <DropdownMenu/>
                </header>
                <Outlet/>
            </div>
        )
    }
}

export default Layout