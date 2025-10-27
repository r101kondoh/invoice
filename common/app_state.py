from abc import ABC
from typing import Any, Generic, List, Optional, TypeVar, final
T = TypeVar("T")

# NOTE: ObserverパターンのSubjectに相当
# 状態の変更を通知する側
class AppState(Generic[T], ABC):
    """
    状態管理クラス
    """
    def __init__(self):
        self.value:Optional[T] = None
        self.observers: List[Any] = []

    def bind(self, view:Any):
        '''
        変更通知を行う相手を設定する
        '''
        if view not in self.observers:
            self.observers.append(view)

    def notify(self):
        '''
        変更通知
        '''
        for o in self.observers:
            o.update(self)

    @final
    def clear(self):
        '''
        ステータスを初期化する
        '''
        if self.value is not None:
            self.value = None
            self.notify

    def set_value(self, value:T):
        '''
        値の設定
        '''
        if self.value != value:
            self.value = value
            self.notify()

    def get_value(self):
        '''
        現在の値を返す
        '''
        return self.value