export default [
  {
    _name: 'CSidebarNav',
    _children: [
      {
        _name: 'CSidebarNavItem',
        name: 'Заполнение',
        to: '/fill/',
        icon: 'cil-speedometer'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Архив',
        to: '/ontologies/',
        icon: 'cil-basket'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Пользователи',
        to: '/users/',
        icon: 'cil-user'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'О программе',
        to: '/about/',
        icon: 'cil-settings'
      },
    ]
  }
]
