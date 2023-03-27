import React from "react";
import Header from "../Header";




class App extends React.Component {
    helpText = "Helpp text!"
    render () {
        return (
            <div className="Name">
                <Header title=" MOI TITEL"/>
                <h1>{this.helpText}</h1>
                <input placeholder={this.helpText}
                       onClick={this.inputClick} onMouseEnter={this.mouseOver}/>
                <p>{this.helpText === "Help text!" ? "yes" : "no"}</p>
            </div>
        )
    }
    inputClick(){console.log("clicked")}
    mouseOver(){console.log("Mouse over")}
}

export default App