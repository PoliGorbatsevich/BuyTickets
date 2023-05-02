import React from 'react';
import {axiosInstance} from "../AxiosConfig";
import {NavLink} from "react-router-dom";
import storage from "../storage";

class DropdownMenu extends React.Component{


    constructor(props) {
        super(props);
        this.state = {
            isMenuOpen: false,
            isLogined: false,
        };
        this.toggleMenu = this.toggleMenu.bind(this);
        this.logOut = this.logOut.bind(this)
    }

    toggleMenu() {
        this.checkLogin();
        this.setState(prevState => ({
            isMenuOpen: !prevState.isMenuOpen
        }));
    }

    checkLogin(){
        axiosInstance.get("/auth/users/me/").then((res) => {
            console.log(res.data)
            this.setState({isLogined: true})
        }).catch(err => {
            this.setState({isLogined: false})
        })
    }

    logOut(){
        this.toggleMenu()
        storage.clearAll();
        this.setState({isLogined: false})
    }


    render(){
        return (
            <div className="dropdown-menu-container">
                <button className="dropdown-menu-button" onClick={this.toggleMenu}>Аккаунт</button>
                {this.state.isMenuOpen && (
                    <ul className="dropdown-menu-list">
                        {this.state.isLogined &&
                        <div>
                            <li className="dropdown-menu-item" onClick={this.toggleMenu}><NavLink to="/user_profile">мой профиль</NavLink></li>
                            <li className="dropdown-menu-item" onClick={this.toggleMenu}><NavLink to="/transaction_history">История транзакций</NavLink></li>
                            <li className="dropdown-menu-item"><NavLink to="/auth" onClick={this.logOut}>выйти</NavLink></li>
                        </div>}
                        {!this.state.isLogined &&
                            <li className="dropdown-menu-item" onClick={this.toggleMenu}><NavLink to="/auth">войти</NavLink></li>}
                    </ul>
                )}
            </div>
        )
    }

}

export default DropdownMenu