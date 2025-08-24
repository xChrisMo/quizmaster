import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <header className='App-header'>
        <div className='header-container'>
          <div className='logo' onClick={() => this.navTo('')}>
            <h1>QuizMaster</h1>
          </div>
          <nav className='nav-menu'>
            <button 
              className='nav-button'
              onClick={() => this.navTo('')}
            >
              Browse
            </button>
            <button 
              className='nav-button'
              onClick={() => this.navTo('/add')}
            >
              Create
            </button>
            <button 
              className='nav-button'
              onClick={() => this.navTo('/play')}
            >
              Play
            </button>
          </nav>
        </div>
      </header>
    );
  }
}

export default Header;
