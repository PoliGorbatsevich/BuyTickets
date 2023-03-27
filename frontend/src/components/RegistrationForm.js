import React from "react";
import toast from "react-hot-toast";

class RegistrationForm extends React.Component{
    user = {
        email: "",
        username: "",
        password: "",
        password1: ""
    }
    constructor(props) {
        super(props);
        this.state = {
            email: "",
            username: "",
            password: "",
            password1: ""
        }
    }
    render(){
        return (
            <div className="base-block">
                <h2>Lets create your account!</h2>
                <form ref={(el) => this.RegForm = el}>
                    <input placeholder="Ваш Email" type="email"
                           onChange={(e) => {this.setState({email: e.target.value})}}/>
                    <input placeholder="Имя пользователя"
                           onChange={(e) => {this.setState({username: e.target.value})}}/>
                    <input placeholder="Пароль" type="password"
                           onChange={(e) => {this.setState({password: e.target.value})}}/>
                    <input placeholder="Пароль еще разок"  type="password"
                           onChange={(e) => {this.setState({password1: e.target.value})}}/>
                    <button type="button" onClick={() => {
                        this.RegForm.reset()
                        if (this.state.password !== this.state.password1)
                            toast.error("Пароли не совпадают")
                        else
                            this.user = {
                                email: this.state.email,
                                username: this.state.username,
                                password: this.state.password,
                                password1: this.state.password1,
                            }
                            this.props.registerUser(this.user)
                        }}>Зарегистрироваться</button>
                </form>
            </div>
        )
    }
}

export default RegistrationForm