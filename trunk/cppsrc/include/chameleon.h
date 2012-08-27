#ifndef EVENT_H
#define EVENT_H
#include <string>
#include <map>
#include <list>
namespace chameleon{
	namespace event{
		typedef void (*callback)(void *);
		class event{
			public:
				event(std::string n, void * d){
					name = n;
					data = d;
				}
				std::string getName(){return name;}
				void setName(std::string name_){name = name_;}
				void *getData(){return data;}
				void setData(void *data_){data = data_;}
			private:
				std::string name;
				void *data;
		};
		template <class T> // We need this so we can create a manager reference in listener.
		class _manager{
			public:
				_manager(){}
				void alert(std::string name, void *data){
					event e(name, data);
					for (typename std::list<T>::iterator it = listeners[e.getName()].begin(); it != listeners[e.getName()].end(); it++){
						(*it)->alert(e);
					}
				}
				void reg(std::string n, T l){
					listeners[n].push_back(l);
				}
                void unregister(std::string n, T l){
					listeners[n].remove(l);
				}
			private:
                std::map<std::string, std::list<T> > listeners;
		};
		template <class T> // T is a function type: either boost::function or boost::python::object.
		class _listener{
			public:
				_listener(){}
				void alert(event e){
					if (responses[e.getName()])
						responses[e.getName()](e.getData());
				}
				void setResponse(std::string n, T c){responses.insert(make_pair(n, c));}
			private:
				std::map<std::string, T> responses;
		};
		typedef _listener<callback> listener;
		typedef _manager<listener *> manager;
	}
}
#endif
