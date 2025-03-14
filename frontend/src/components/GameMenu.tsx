import type { Component } from 'solid-js';
import styles from './GameMenu.module.css'

const GameMenu: Component = () => {
    const createNewGame = () => {
        console.log("New Game Started!");
    }
    return (
        <div class={styles.App}>
            <h1 class={styles.gameMenuTitle}>Football Sim</h1>
            <div class={styles.gameMenuButtons}>
                <button classList={{ [styles.gameMenuButton]: true, [styles.gameMenuContinue]: true }}>
                    Continue
                </button>
                <button classList={{ [styles.gameMenuButton]: true, [styles.gameMenuNewGame]: true }}
                    onClick={() => createNewGame()}
                >
                    New Game
                </button>
            </div>
        </div>
    );
};

export default GameMenu;