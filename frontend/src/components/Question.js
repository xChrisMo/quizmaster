import React, { Component } from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
    };
  }

  flipVisibility() {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className='question-card'>
        <div className='question-header'>
          <div className='question-text'>{question}</div>
          <div className='question-meta'>
            <div className='category-badge'>
              <img
                alt={`${category ? category.toLowerCase() : 'unknown'}`}
                src={`${category ? category.toLowerCase() : 'unknown'}.svg`}
              />
              <span>{category || 'Unknown'}</span>
            </div>
            <div className='difficulty-badge'>
              Level {difficulty}
            </div>
            <button
              className='delete-button'
              onClick={() => this.props.questionAction('DELETE')}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
            </button>
          </div>
        </div>
        
        <div className='question-actions'>
          <button
            className='answer-toggle'
            onClick={() => this.flipVisibility()}
          >
            {this.state.visibleAnswer ? 'Hide Answer' : 'Show Answer'}
          </button>
        </div>
        
        {this.state.visibleAnswer && (
          <div className='answer-section'>
            <div className='answer-text'>
              <strong>Answer:</strong> {answer}
            </div>
          </div>
        )}
      </div>
    );
  }
}

export default Question;
