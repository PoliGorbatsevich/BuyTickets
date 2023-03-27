import React from "react";

class ChangePassword extends React.Component{
    user = {}
    constructor(props) {
        super(props);
        this.state = {
            user: {
                old_password:"",
                password: "",
                password1: ""
            }
        }
    }
    render(){
        return (
            <div className="base-block">
                <h2>Поменять пароль</h2>
                <form ref={(el) => this.form = el}>
                    <input placeholder="Старый Пароль"
                           onChange={(e) => {this.setState({old_password: e.target.value})}}/>
                    <input placeholder="Новый Пароль"
                           onChange={(e) => {this.setState({password: e.target.value})}}/>
                    <input placeholder="Новый Пароль еще разок"
                           onChange={(e) => {this.setState({password1: e.target.value})}}/>
                    <button type="button" onClick={() => {
                        this.form.reset()
                        if (this.state.password === this.state.password1)
                            this.props.changePass(this.state.old_password, this.state.password, this.state.password1)
                    }}>Изменить пароль</button>
                </form>
            </div>
        )
    }
}

export default ChangePassword