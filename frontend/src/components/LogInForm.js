import React from "react";

class LogInForm extends React.Component{
    user = {
        username: "",
        password: "",
    }
constructor(props) {
        super(props);
        this.state = {
                username: "",
                password: "",
        }
    }
    render(){
        return (
            <div className="base-block">
                <h2>Lets Log in!</h2>
                <form ref={(el) => this.RegForm = el}>
                    <input placeholder="Имя пользователя"
                           onChange={(e) => {this.setState({username: e.target.value})}}/>
                    <input placeholder="Пароль" type="password"
                           onChange={(e) => {this.setState({password: e.target.value})}}/>
                    <button type="button" onClick={() => {
                        this.RegForm.reset()
                            this.user = {
                                username: this.state.username,
                                password: this.state.password,
                            }
                        this.props.loginUser(this.user)
                    }}>Войти</button>
                </form>
            </div>
        )
    }
}

export default LogInForm