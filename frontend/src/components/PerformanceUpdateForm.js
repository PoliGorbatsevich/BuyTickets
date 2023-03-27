import React from "react";

class PerformanceUpdateForm extends React.Component{
    performance = {}
    constructor(props) {
        super(props);
        this.state = {
            name: "",
            description: "",
            date: "",
            time: ""
        }
    }
    render(){
        return (
            <form ref={(el) => this.MyForm = el}>
                <input placeholder="Название пьесы"
                       onChange={(e) => {this.setState({name: e.target.value})}}/>
                <textarea placeholder="Описание"
                          onChange={(e) => {this.setState({description: e.target.value})}}/>
                <input placeholder="Дата" type="date"
                       onChange={(e) => {this.setState({date: e.target.value})}}/>
                <input placeholder="Время" type="time"
                       onChange={(e) => {this.setState({time: e.target.value})}}/>
                <button type="button" onClick={() => {
                    this.MyForm.reset()
                    this.performance = {
                        name: this.state.name,
                        description: this.state.description,
                        date: this.state.date,
                        time: this.state.time,
                    }
                    this.props.onUpdate(this.props.id, this.performance)
                }}>Добавить</button>
            </form>
        )
    }
}

export default PerformanceUpdateForm