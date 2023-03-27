import React from "react";

class AddPerformance extends React.Component{
    addPerformance = {}
    constructor(props) {
        super(props);
        this.state = {
            name: "",
            description: "",
            date: "",
            time: "",
            rowCount: 1,
            rowLength: 1,
        }
    }
    render(){
        return (
            <form ref={(el) => this.MyForm = el}>
                <input placeholder="Название пьесы"
                       onChange={(e) => {this.setState({name: e.target.value})}}/>
                <textarea placeholder="Описание"
                          onChange={(e) => {this.setState({description: e.target.value})}}/>
                <input placeholder="Дата"
                       onChange={(e) => {this.setState({date: e.target.value})}}/>
                <input placeholder="Время"
                       onChange={(e) => {this.setState({time: e.target.value})}}/>
                <input placeholder="Количество рядов"
                       onChange={(e) => {this.setState({rowCount: e.target.value})}}/>
                <input placeholder="Длина ряда"
                       onChange={(e) => {this.setState({rowLength: e.target.value})}}/>
                <button type="button" onClick={() => {
                    this.MyForm.reset()
                    this.addPerformance = {
                        name: this.state.name,
                        description: this.state.description,
                        date: this.state.description,
                        time: this.state.time,
                        rowCount: this.state.rowCount,
                        rowLength: this.state.rowLength
                    }
                    if (this.props.performance)
                        this.addPerformance.id = this.props.performance.id
                    this.props.onAdd(this.addPerformance)
                }}>Добавить</button>
            </form>
        )
    }
}

export default AddPerformance