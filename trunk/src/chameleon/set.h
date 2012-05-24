#ifndef SET_H
#define SET_H
#include <boost/function.hpp>
#include <assert.h>
using namespace std;
namespace cham{
	namespace util{
		template<class T>
		class node {
			public:
				node(T info) {
					data = info;
					nextPtr = 0;
				}
				T getData(){return data;}
				cham::util::node<T> *nextPtr;
			private:
				T data;
		};
		template<class T>
		class list {
			public:
				list(){
					firstPtr = lastPtr = 0;
					len = 0;
				}
				~list(){
					if (!isEmpty()){
						cham::util::node<T> *currentPtr = firstPtr, *tempPtr;
						while (currentPtr != 0){
							tempPtr = currentPtr;
							currentPtr = currentPtr->nextPtr;
							delete tempPtr;
						}
					}
				}
				void push(T value){
					cham::util::node<T> *newPtr = getNewNode(value);
					if (isEmpty())
						firstPtr = lastPtr = newPtr;
					else {
						newPtr->nextPtr = firstPtr;
						firstPtr = newPtr;
					}
					len += 1;
				}
				void append(T value){
					cham::util::node<T> *newPtr = getNewNode(value);
					if (isEmpty())
						firstPtr = lastPtr = newPtr;
					else {
						lastPtr->nextPtr = newPtr;
						lastPtr = newPtr;
					}
					len += 1;
				}
				bool popf(){
					if (isEmpty())
						return 0;
					else {
						if (firstPtr == lastPtr)
							firstPtr = lastPtr = 0;
						else
							firstPtr = firstPtr->nextPtr;
						len -= 1;
						return 1;
					}
				}
				bool popb(){
					if (isEmpty())
						return 0;
					else {
						if (firstPtr == lastPtr)
							firstPtr = lastPtr = 0;
						else {
							cham::util::node<T> *currentPtr = firstPtr;
							while (currentPtr->nextPtr != lastPtr)
								currentPtr = currentPtr->nextPtr;
							lastPtr = currentPtr;
							currentPtr->nextPtr = 0;
						}
						len -= 1;
						return 1;
					}
				}
				bool isEmpty() const {return firstPtr == 0;}
				T operator[](int subscript){
					assert(subscript <= len - 1 && subscript >= 0);
					cham::util::node<T> *currentPtr = firstPtr;
					for (int counter = 0; counter != subscript; counter++){
						currentPtr = currentPtr->nextPtr;
					}
					return currentPtr->getData();
				}
				int getLen() const {return len;}
				int len;
				node<T> *firstPtr;
				node<T> *lastPtr;
				node<T> *getNewNode(T value){
					node<T> *ptr = new node<T>(value);
					assert(ptr != 0);
					return ptr;
				}
		};
		template<class T>
		class set{
			public:
				set(){}
				bool in(T value){
					int counter = 0;
					for (cham::util::node<T> *temp = base.firstPtr; counter < base.getLen(); temp = temp->nextPtr){
						if (temp->getData() == value){
							return 1;
						}
						counter++;
					}
					return 0;
				}
				void apply(boost::function<void (T val)> func){
					int counter = 0;
					for (cham::util::node<T> *temp = base.firstPtr; counter < base.getLen(); temp = temp->nextPtr){
						func(temp->getData());
						counter++;
					}
				}
				void add(T value){base.append(value);}
				void remove(T value){
					cham::util::node<T> *prev;
					int counter = 0;
					for (cham::util::node<T> *temp = base.firstPtr; counter < base.getLen(); temp = temp->nextPtr){
						if (temp->getData() == value){
							if (temp == base.firstPtr){
								cham::util::node<T> *t = base.firstPtr;
								base.firstPtr = base.firstPtr->nextPtr;
								delete t;
								return;
							}
							else{
								prev->nextPtr = temp->nextPtr;
								delete temp;
								return;
							}
						}
						prev = temp;
						counter++;
					}
				}
				int size(){return base.getLen();}
				void empty(){
					while (!base.isEmpty()){
						base.popf();
					}
				}
				bool operator==(set<T> o){
					int counter = 0;
					if (base.getLen() != o.size()){
						return 0;
					}
					for (cham::util::node<T> *temp = base.firstPtr; counter < base.getLen(); temp = temp->nextPtr){
						if (!(temp->getData() == o[counter])){
							return 0;
						}
						counter++;
					}
					return 1;
				}
				T operator[](int s){return base[s];}
			private:
				list<T> base;
		};
	}
}
#endif
