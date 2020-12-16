import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { compose } from 'redux';
import { createStructuredSelector } from 'reselect';
import classNames from 'classnames';
import isEqual from 'lodash/isEqual';

import BowlRice from 'components/pages/game/BowlRice';
import PageContainer from 'components/pages/common/PageContainer';
import Question from 'components/pages/game/Question';
import Globe from 'components/pages/game/Globe';
import AdBlock from 'components/app/AdBlock/AdBlock';
import BodyHeight from 'components/app/MobileBodyHeight';
import MigrateTotalsBlock from 'components/app/MigrateTotalsBlock';
import GetTheApp from 'components/app/GetTheApp';
import GameStatistics from 'components/pages/common/GameBlocks/GameStatistics';
import GlobalStats from 'components/pages/common/GameBlocks/GlobalStats';
import { withNotification, LARGE_NOTIFICATION, SMALL_NOTIFICATION } from 'components/app/Notification';
import { withTabOrder, tabOrders, TAB_NAMES } from 'components/app/TabOrder';

import {
  createGame,
  loadGame,
  submitAnswer,
  getGameID,
  getGameCategory,
  getGameLevel,
  getGameRiceCount,
  getCurrentQuestion,
  getPrevQuestion,
  getLastAnswer,
  isGameLoading,
  getGameError,
  changeCategory,
  getGameNotifications,
  loadAdList,
} from '@wfp/freerice-core/modules/game';
import { getCategories } from '@wfp/freerice-core/modules/categories';
import { getUserID, getUserAccount } from '@wfp/freerice-core/modules/user';
import { getYesterdayRice, loadGlobalStats } from '@wfp/freerice-core/modules/leaderboard';
import { getLevels } from '@wfp/freerice-core/modules/levels';
import { getLanguage } from '@wfp/freerice-core/modules/app';
import strings from 'res/strings';


class Game extends Component {
  static propTypes = {
    category: PropTypes.object.isRequired,
    createGame: PropTypes.func.isRequired,
    loadGame: PropTypes.func.isRequired,
    changeCategory: PropTypes.func.isRequired,
    submitAnswer: PropTypes.func.isRequired,
    gameId: PropTypes.string,
    categories: PropTypes.array,
    levels: PropTypes.array.isRequired,
    level: PropTypes.number,
    rice: PropTypes.number,
    question: PropTypes.object,
    prevQuestion: PropTypes.object,
    answer: PropTypes.object,
    loading: PropTypes.bool,
    user: PropTypes.string,
    userAccount: PropTypes.object,
    yesterdayRice: PropTypes.number,
    loadGlobalStats: PropTypes.func.isRequired,
    setNotificationVisibility: PropTypes.func.isRequired,
    match: PropTypes.object.isRequired,
    language: PropTypes.string,
    setTabOrder: PropTypes.func.isRequired,
    focusTo: PropTypes.func.isRequired,
    notifications: PropTypes.array.isRequired,
    location: PropTypes.object.isRequired,
    loadAdList: PropTypes.func.isRequired,
  };

  static defaultProps = {
    gameId: null,
    categories: [],
    level: 1,
    rice: 0,
    question: null,
    prevQuestion: null,
    answer: null,
    loading: false,
    user: null,
    userAccount: null,
    yesterdayRice: null,
    language: strings.getLanguage(),
  };

  state = {
    viewMode: 'question',
    selection: null,
    focusQuestionAfterReload: false,
  };

  static getDerivedStateFromProps(nextProps, prevState) {
    // switch viewMode to 'answer' in order to display prevQuestion and it's selection/answer.
    if (nextProps.loading && nextProps.prevQuestion && prevState.selection) {
      return { viewMode: 'answer' };
    }
    return null;
  }

  componentDidMount() {
    const {
      gameId,
      question,
      category,
      categories,
      createGame,
      loadGame,
      changeCategory,
      level,
      user,
      yesterdayRice,
      loadGlobalStats,
      match,
      language,
      setTabOrder,
      focusTo,
      location,
      loadAdList,
    } = this.props;

    setTabOrder(tabOrders.GAME);

    if (location.state && location.state.focusAfter) focusTo(TAB_NAMES.MENU_TOGGLE);

    const categoryFromRouter = categories.find((category) => category.machine_name === match.params.category);

    // Redirect if category doesn't exist
    if (match.params.category && !categoryFromRouter) window.location.href = '/game';

    if (!gameId) {
      if (categoryFromRouter) {
        createGame(categoryFromRouter ? categoryFromRouter.id : null, level, user, language);
      } else {
        createGame(category ? category.id : null, level, user, language);
      }
    } else if (!question) {
      if (categoryFromRouter && categoryFromRouter.id !== category.id) {
        changeCategory(gameId, { category: categoryFromRouter.id, level: 1 }, language);
      } else {
        loadGame(gameId, language);
      }
    }

    loadAdList();

    if (!user || !yesterdayRice) {
      loadGlobalStats();
    }
  }

  componentDidUpdate(prevProps) {
    const { loading, answer, setNotificationVisibility, focusTo, notifications } = this.props;
    const { viewMode, focusQuestionAfterReload } = this.state;

    // show answering results for some time and then switch to next question.
    if (!loading && prevProps.loading && viewMode === 'answer') {
      setTimeout(() => {
        this.setState({ selection: null, viewMode: 'question', focusQuestionAfterReload: false });

        if (focusQuestionAfterReload) {
          setTimeout(() => {
            focusTo(TAB_NAMES.QUESTION_TEXT);
          }, 600);
        }
      }, answer.correct ? 1400 : 2800);
    }

    if (notifications && notifications.length && !isEqual(notifications, prevProps.notifications)) {
      if (notifications[0].size === 'large') setNotificationVisibility(LARGE_NOTIFICATION, true, notifications[0]);
      else setNotificationVisibility(SMALL_NOTIFICATION, true, notifications[0]);
    }
  }

  handleAnswer = (answer, focusQuestionAfterReload = false) => {
    const { gameId, submitAnswer, question, user, category, language } =  

    if (typeof window.gtag === 'function') {
      window.gtag('event', 'answer_question', { 'event_category': category.machine_name });
    }

    this.setState({ selection: answer, focusQuestionAfterReload }, () => {
      submitAnswer(gameId, { answer, question: question.id, user }, language);
    });
  };

  render() {
    const { selection, viewMode } = this.state;
    const {
      category,
      levels,
      level: levelNumber = 1,
      question,
      prevQuestion,
      answer,
      rice,
      user,
      userAccount,
      yesterdayRice,
      language,
    } = this.props;
    const level = levels.find(l => l.levels === levelNumber);
    const displayQuestion = viewMode === 'answer' ? prevQuestion : question;
    const pageGameClass = language === 'ar' ? 'page--game-rtl' : 'page--game';

    return (
      <PageContainer className={classNames(pageGameClass, { 'is-anonymous': !user })}>
        <BodyHeight>
          {height => (
            <div className="page__body" style={{ minHeight: height && `${height - 45}px` }}>
              <MigrateTotalsBlock />
              <div className="statistics">
                {!!user && <GameStatistics user={userAccount} />}
                <GlobalStats yesterdayRice={yesterdayRice} />
              </div>
              <GetTheApp />

              <div className="game-block">
                {!!displayQuestion && (
                  <Question
                    onAnswer={this.handleAnswer}
                    question={displayQuestion}
                    answer={answer}
                    selection={selection}
                  />
                )}

                <Globe>
                  <BowlRice riceCount={rice} category={category} level={level} />
                </Globe>
              </div>
              {!!question && <AdBlock isCorrectAnswer={answer.correct} key={question.id} />}
            </div>
          )}
        </BodyHeight>
      </PageContainer>
    );
  }
}

export default compose(
  withTabOrder,
  withNotification,
  connect(
    createStructuredSelector({
      category: getGameCategory,
      categories: getCategories,
      gameId: getGameID,
      levels: getLevels,
      level: getGameLevel,
      rice: getGameRiceCount,
      question: getCurrentQuestion,
      prevQuestion: getPrevQuestion,
      answer: getLastAnswer,
      loading: isGameLoading,
      error: getGameError,
      user: getUserID,
      userAccount: getUserAccount,
      yesterdayRice: getYesterdayRice,
      language: getLanguage,
      notifications: getGameNotifications,
    }),
    { createGame, loadGame, submitAnswer, loadGlobalStats, changeCategory, loadAdList }
  )
)(Game);
